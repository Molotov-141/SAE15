import markdown
import sys

def convert(fichiermd, fichierhtml):
    '''convertit un fichier .md en fichier .html'''
    with open(fichiermd, 'r') as f: ## ouverture du fichier et extraction du contenu
        text = f.read()  ## stockage du contenu

    html = markdown.markdown(text) ## convertion md -> html

    with open(fichierhtml, 'w') as f: ## creation et ecriture dans un fichier en .html
        f.write("<html><head><meta charset='utf-8'><link rel='stylesheet' type='text/css' href='style.css'></head><body>")
        f.write(html)
        f.write("</body></html>")


if __name__ == '__main__': ## execution que dans le bash
    convert(sys.argv[1],sys.argv[2])