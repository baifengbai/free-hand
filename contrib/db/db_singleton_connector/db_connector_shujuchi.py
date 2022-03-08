from .db_connector_default import DB_Singleton_DEFAULT

class DB_Singleton_Shujuchi(DB_Singleton_DEFAULT):
    def insert_key_paragraph(self, ori_uri, paragraph, tag_origin, publish_time, crawl_time, site, classfication):
        pass

    def insert_relative_paragraph(self, ori_uri, paragraph, publish_time, crawl_time, site, classfication):
        pass

    def insert_comment(self, ori_uri, comment, publish_time, crawl_time, site, classfication):
        pass

    def insert_article(self, ori_uri, title, content, publish_time, crawl_time, site, classfication):
        pass

    def insert_img(self, img_type, ori_uri, reco, crawl_time, local_path, site, classfication):
        pass

    def insert_video(self, ori_uri, title, publish_time, crawl_time, local_path, site, classfication):
        pass

    def insert_selenium_info(self, executor, session_id):
        pass

    def insert_site_info(self, crawl_type, site, site_url, site_usable, comment, classfication):
        pass

    def insert_stocks(self, name, code, belonging, ishot):
        pass