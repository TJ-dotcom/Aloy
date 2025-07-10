
import os
import google.generativeai as genai
import typer
from pathlib import Path
from compiler import prompts

app = typer.Typer()

def clean_generated_content(content: str, file_type: str) -> str:
    """Clean up markdown artifacts and unwanted formatting from generated content."""
    if not content:
        return content
    
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        stripped_line = line.strip()
        
        # Remove markdown code block markers - be more aggressive
        if (stripped_line.startswith('```') or 
            stripped_line in ['```yaml', '```dockerfile', '```ignore', '```', '```bash', '```shell', '```text'] or
            stripped_line.endswith('```')):
            continue
            
        cleaned_lines.append(line)
    
    # Remove empty lines at the beginning and end
    while cleaned_lines and not cleaned_lines[0].strip():
        cleaned_lines.pop(0)
    while cleaned_lines and not cleaned_lines[-1].strip():
        cleaned_lines.pop()
    
    result = '\n'.join(cleaned_lines)
    
    # Additional cleanup - remove any remaining standalone ``` lines
    result = result.replace('\n```\n', '\n')
    result = result.replace('\n```', '')
    result = result.replace('```\n', '')
    
    # If the content starts or ends with ```, remove them
    if result.startswith('```'):
        result = result[3:].lstrip()
    if result.endswith('```'):
        result = result[:-3].rstrip()
    
    return result

def generate_from_prompt(model, prompt_template: str, context: str) -> str:
    """Calls the LLM API to generate file content."""
    try:
        # Handle both old format {requirements_content} and new format {full_context}
        if "{full_context}" in prompt_template:
            formatted_prompt = prompt_template.format(full_context=context)
        else:
            formatted_prompt = prompt_template.format(requirements_content=context)
            
        response = model.generate_content(
            formatted_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2
            )
        )
        
        raw_content = response.text.strip()
        
        # Determine file type for cleaning
        file_type = "unknown"
        if "dockerfile" in prompt_template.lower():
            file_type = "dockerfile"
        elif "yaml" in prompt_template.lower() or "gitlab" in prompt_template.lower():
            file_type = "yaml"
        elif "ignore" in prompt_template.lower():
            file_type = "ignore"
        
        # Clean the content
        cleaned_content = clean_generated_content(raw_content, file_type)
        
        return cleaned_content
    except Exception as e:
        typer.secho(f"Error calling Gemini API: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def main(
    source_path: Path = typer.Argument(
        ..., 
        exists=True, 
        file_okay=False, 
        dir_okay=True, 
        resolve_path=True,
        help="Path to the source directory of the Python project."
    ),
    model_name: str = typer.Option(
        "gemini-2.5-pro",
        "--model",
        "-m",
        help="The Gemini AI model to use for generation."
    )
):
    """
    The Engineer's Intent Compiler 🚀
    Generates a Dockerfile, .dockerignore, and gitlab-ci.yml from your project's intent.
    """

    typer.echo(f"▶️ Starting compilation for project at: {source_path}")

    # 1. Check for and read requirements.txt

    requirements_path = source_path / "requirements.txt"
    if not requirements_path.is_file():
        typer.secho("Error: requirements.txt not found in the source directory.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    requirements_content = requirements_path.read_text()
    typer.echo("✅ Found and read requirements.txt.")
    
    project_files = [p.name for p in source_path.iterdir() if p.is_file()]
    file_list_str = "\n".join(project_files)
    full_context = f"""
**Analysis Context:**

The user's project has the following `requirements.txt`:
<requirements>
{requirements_content}
</requirements>

And the following files in its root directory:
<project_files>
{file_list_str}
</project_files>
"""

    # 2. Set up Gemini Client

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        typer.secho("Error: GOOGLE_API_KEY environment variable not set.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    # 3. Generate each file
    file_generation_tasks = {
        "Dockerfile": prompts.DOCKERFILE_PROMPT,
        ".dockerignore": prompts.DOCKERIGNORE_PROMPT,
        "gitlab-ci.yml": prompts.GITLAB_CI_PROMPT,
    }


    for filename, prompt in file_generation_tasks.items():
        typer.echo(f"⏳ Generating {filename}...")
        try:
            generated_content = generate_from_prompt(model, prompt, full_context)
        except Exception as e:
            continue
        
        # Additional cleanup based on filename
        if filename.lower() == "dockerfile":
            generated_content = clean_generated_content(generated_content, "dockerfile")
        elif filename.endswith(".yml") or filename.endswith(".yaml"):
            generated_content = clean_generated_content(generated_content, "yaml")
        elif "ignore" in filename.lower():
            generated_content = clean_generated_content(generated_content, "ignore")
        
        if not generated_content or len(generated_content) < 15:
            typer.secho(f"⚠️ Warning: Received invalid or empty content for {filename}. Skipping file creation.", fg=typer.colors.YELLOW)
            continue
        
        # 4. Write file to disk
        output_path = source_path / filename
        output_path.write_text(generated_content)
        typer.secho(f"✅ Successfully created {filename} at {output_path}", fg=typer.colors.GREEN)

    typer.secho("\n🎉 Compilation complete!", fg=typer.colors.BRIGHT_GREEN, bold=True)

# Ensure Typer CLI runs when script is executed directly
if __name__ == "__main__":
    app()
