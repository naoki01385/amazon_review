from selenium import webdriver
from selenium .webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import textwrap
import time

def get_amazon_page_info(url):
    text = ""                               #　初期化
    options = Options()                     #　オプションを用意
    options.add_argument('--incognito')     #　シークレットモードの設定を付与
    #　chromedriverのパスとパラメータを設定
    driver = webdriver.Chrome("/Users/naoki/Jupyter/jupyter_hub_function/chromedriver4",options=options)
    driver.get(url)                         #　chromeブラウザでurlを開く
    driver.implicitly_wait(10)              #　指定したドライバの要素が見つかるまでの待ち時間を設定
    text = driver.page_source               #　ページ情報を取得
    
    driver.quit()                           #　chromeブラウザを閉じる
    
    return text                             #　取得したページ情報を返す
 
# 全ページ分をリストにする
def get_all_reviews(url):
    review_list = []                        #　初期化
    i = 1                                   #　ループ番号の初期化
    while True:
        print(i,'page_search')              #　処理状況を表示
        i += 1                              #　ループ番号を更新
        text = get_amazon_page_info(url)    #　amazonの商品ページ情報(HTML)を取得する
        amazon_bs = BeautifulSoup(text, features='lxml')    #　HTML情報を解析する
        reviews = amazon_bs.select('.review-text')         
        
        for review in reviews: 
            review_list.append(review)     
                            
        next_page = amazon_bs.select('li.a-last a')         
        
        # 次のページが存在する場合
        if next_page != []: 
            # 次のページのURLを生成   
            next_url = 'https://www.amazon.co.jp/' + next_page[0].attrs['href']    
            url = next_url  # 次のページのURLをセットする
            
            time.sleep(1)        # 最低でも1秒は間隔をあける(サーバへ負担がかからないようにする)
        else:               # 次のページが存在しない場合は処理を終了
            break
 
    return review_list
 
#インポート時は実行されないように記載
if __name__ == '__main__':
     
    #　Amzon商品ページ
    url = 'https://www.amazon.co.jp/%E6%89%8B%E6%8C%87%E6%B6%88%E6%AF%92%E5%89%A4%E3%80%91%E3%83%8F%E3%83%B3%E3%83%89%E3%82%B9%E3%82%AD%E3%83%83%E3%82%B7%E3%83%A5EX-%E3%81%A4%E3%81%91%E3%81%8B%E3%81%88%E7%94%A8-800ml-%E8%8A%B1%E7%8E%8B%E3%83%97%E3%83%AD%E3%83%95%E3%82%A7%E3%83%83%E3%82%B7%E3%83%A7%E3%83%8A%E3%83%AB%E3%82%B7%E3%83%AA%E3%83%BC%E3%82%BA-%E6%8C%87%E5%AE%9A%E5%8C%BB%E8%96%AC%E9%83%A8%E5%A4%96%E5%93%81/dp/B005RUI15O/'
    
    # URLをレビューページのものに書き換える
    review_url = url.replace('dp', 'product-reviews')
    # レビュー情報の取得
    review_list = get_all_reviews(review_url)    
    
    for i in range(len(review_list)):
        rvw_text=textwrap.fill(review_list[i].text,80)
        print ('\nNo.{} :'.format(i+1))
        print(rvw_text)





