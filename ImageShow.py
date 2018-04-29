class ImageShow:
    def __init__(self):
        self.path="index.html"
        self.images_file="duplicate_images_path.txt"
        self.images_html_text=''

    def write_to_html(self):
        f = open(self.path, 'w')
        message = """<html>
        <head></head>
        <body><p>Duplicate Images. Pick and Delete <p>"""+self.images_html_text+"""</body></html>"""
        f.write(message)
        f.close()

    def get_content_from_file(self):
        f=open(self.images_file,'r')
        image_path=''
        for line in f.readlines():
            image_path="""<img src='"""+line+"""' width="400" height="400"/>"""
            self.images_html_text=self.images_html_text+image_path
            print self.images_html_text


def main():
    imageshow=ImageShow()
    imageshow.get_content_from_file()
    imageshow.write_to_html()

if __name__=="__main__":
    main()
