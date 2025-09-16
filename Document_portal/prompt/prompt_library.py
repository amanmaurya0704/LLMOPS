from langchain_core.prompts import ChatPromptTemplate


document_analysis_prompt = ChatPromptTemplate.from_template("""
You are a highly capable assistant trained to analyse and summarise documents.
Return ONLY Valid Json matching the excat schema below.

{format_instructions}

Analyse this document:
{document_text}
""")

document_comparison_prompt = ChatPromptTemplate.from_template("""
You will be provided with content from two PDFs. You tasks are as follows:

1. Compare the content in two PDFs.
2. Identify the difference in PDF and note down the page number.
3. The output you provide must be page wise comparison
4. If any page do not have any change, mention no change.

Input document:

{combined_docs}

Your response should follow this format:

{format_instruction}
""")

PROMPT_REGISTRY = {
    "document_analysis" : document_analysis_prompt,
    "document_comparision": document_comparison_prompt
}