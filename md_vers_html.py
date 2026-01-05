import markdown

def md_to_html():
    with open(a_def, 'r') as f: ## ouverture du fichier et extraction du contenu
        text = f.read()  ## stockage du contenu

    html = markdown.markdown(text) ## convertion md -> html

    with open('a_def_aussi.html', 'w') as f: ## creation et ecriture dans un fichier en .html
        f.write(html)
