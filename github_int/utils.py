def extract_code_from_pr(files):
    combined = []

    for file in files:
        patch = file.get("patch")
        if patch:
            combined.append(
                f"File: {file['filename']}\n{patch}"
            )

    return "\n\n".join(combined)
