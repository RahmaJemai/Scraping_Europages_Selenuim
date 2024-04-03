from selenium import webdriver
import time
import pandas as pd
import os
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

url = "https://www.europages.fr/entreprises/cat-1-d%C3%A9veloppement%20web/france/soci%C3%A9t%C3%A9s%20de%20d%C3%A9veloppement%20web.html"


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--remote-debugging-port=9222')

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)
driver.get(url)

def collect_companies(url):
    companies = []
    for page in range(1, 5):
        page_url = url.format(page)
        driver.get(page_url)
        company_elements = driver.find_elements(By.CSS_SELECTOR, "li.ep-ecard.text-start.rounded.theme--light.text-decoration-none.pa-5.ep-ecard-serp.mb-3.mb-lg-6.elevation-2")
        for company in company_elements:
            company_link = company.find_element(By.CLASS_NAME, "ep-ecard-serp__epage-link")
            company_url = company_link.get_attribute("href")
            company_name_element = company.find_element(By.CSS_SELECTOR, "p.text-subtitle-1.font-weight-black.pa-3.pb-0.ma-0")
            company_name = company_name_element.text
            companies.append((company_url, company_name))
    return companies


def collect_url(url):
    list_url = []
    for company_url, company_name in collect_companies(url):
        list_url.append((company_url, company_name))
    return list_url


def collect_info(urls):
  all_data = []
  for url in urls:
    url_specific_data = {}
    url_specific_data['Url'] = url[0]
    url_specific_data['Name'] = url[1]
    try:
        print("Fetching information for:", url)
        driver.get(url[0])
        #collect description
        try:
           description = driver.find_element(By.CLASS_NAME, "ep-text-with-overflow__text").text
           url_specific_data['Description'] = description
        except Exception as e:
           print("information not found for URL:", url)

        #collect web site
        try:
           element = driver.find_element(By.CSS_SELECTOR, "a.ep-buttons-mobile-navigation__website-button")
           url_web_site = element.get_attribute('href')
           url_specific_data['Web Site'] = url_web_site
        except Exception as e:
           print("information not found for URL:", url)


        #collect address
        try:
           address_elements = driver.find_elements(By.CSS_SELECTOR, "div.v-card__text p.text--primary.ma-0")
           url_specific_data['Address'] =  ' '.join([element.text.strip() for element in address_elements])
        except Exception as e:
           print("information not found for URL:", url)


        #collect delivery zone
        try:
          zone = driver.find_element(By.CSS_SELECTOR, "div.ep-epages-home-trading-areas > ul > li:nth-child(1) > span.ep-epages-home-trading-areas__text")
          trading_area = zone.text
          url_specific_data['Zone Livraison'] = trading_area
        except Exception as e:
            print("information not found for URL:", url)


        #collect phone
        try:
          driver.execute_script("document.getElementById('cookiescript_injected_wrapper').style.display = 'none';")

          button = driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div[1]/div/div[2]/div[1]/header/div[3]/div[1]/button[1]")
          button.click()

          phone_container = driver.find_element(By.CSS_SELECTOR, 'div.ep-epage-sidebar-phone-popup__container')

          afficher_numero_button = phone_container.find_element(By.CSS_SELECTOR, 'button.ep-epage-phone-popup-number__button')
          afficher_numero_button.click()

          phone_number_button = phone_container.find_element(By.CSS_SELECTOR, 'button.ep-epage-phone-popup-number__button')
          phone_number = phone_number_button.find_element(By.CSS_SELECTOR, 'span.ep-epage-phone-popup-number__button-text').text
          url_specific_data['Numero'] = phone_number
        except Exception as e:
           print("numero not found for URL:", url)

        #collect products
        try:
          link_element = driver.find_element(By.XPATH, '//a[@class="ep-arrow-link text-decoration-none"]')
          link_href = link_element.get_attribute('href')
          driver.get(link_href)
          title_elements = driver.find_elements(By.CSS_SELECTOR, 'div.pa-0.ep-page-epage-catalog__cards div.ep-product-card figcaption')
          list_product = []
          for title_element in title_elements:
              title_text = title_element.text
              list_product.append(title_text)
              
          url_specific_data['Produits'] = list_product
        except Exception as e:
          print("information not found for URL:", url)


        driver.get(url[0])
        #collect activites
        try:
           wait = WebDriverWait(driver, 10)
           ul_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul.ep-keywords__list')))
           wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ul.ep-keywords__list li')))
           items = [li_element.text for li_element in ul_element.find_elements(By.CSS_SELECTOR, 'li.ep-keywords__list-item')]
           url_specific_data['Activites'] = items

           button_xpath = "//button[@class='ep-show-more-less mt-2 v-btn v-btn--text theme--light v-size--x-small']"
           try:
              driver.execute_script("document.getElementById('cookiescript_injected_wrapper').style.display = 'none';")
              button = driver.find_element(By.XPATH, button_xpath)
              button.click()
              wait = WebDriverWait(driver, 10)
              ul_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul.ep-keywords__list')))
              wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ul.ep-keywords__list li')))
              new_items = [li_element.text for li_element in ul_element.find_elements(By.CSS_SELECTOR, 'li.ep-keywords__list-item')]
              url_specific_data['Activites'] = new_items
           except Exception as e:
              print("button not found for URL:", url)
        except Exception as e:
           print("activite not found for URL:", url)


        #collect infos
        try:
          print("Fetching information for:", url)
          organisation = driver.find_element(By.CSS_SELECTOR, "div.ep-key-value-list.ep-epages-home-business-details__list-column.ep-epages-home-business-details__organization")
          try:
             annee_creation = organisation.find_element(By.CSS_SELECTOR, "li.ep-key-value.ep-epages-business-details-year-established dl.ep-key-value__content dd.ep-key-value__value").text
             url_specific_data['annee creation'] = annee_creation
          except:
             print("Annee de creation non trouvee pour l'URL:", url)

          try:
             activite_principale = organisation.find_element(By.CSS_SELECTOR, 'li.ep-key-value.ep-epages-business-details-main-activity > dl.ep-key-value__content > dd.ep-key-value__value').text
             url_specific_data['activite principale'] = activite_principale
          except:
             print("Activite principale non trouvee pour l'URL:", url)

          try:
             nature_entreprise = organisation.find_element(By.CSS_SELECTOR, "li.ep-key-value.ep-epages-business-details-site-status dl.ep-key-value__content dd.ep-key-value__value.text-body-1").text
             url_specific_data['nature entreprise'] = nature_entreprise
          except:
            print("Nature de l'entreprise non trouvee pour l'URL:", url)

        except Exception as e:
           print("information not found for URL:", url)

        try:
          chiffres_cles = driver.find_element(By.CSS_SELECTOR, "div.ep-epages-home-business-details__list-column.ep-epages-home-business-details__key-figures")
          try:
              effectif = chiffres_cles.find_element(By.CSS_SELECTOR, "li.ep-key-value.ep-epages-business-details-headcount dl.ep-key-value__content dd.ep-key-value__value").text
              url_specific_data['effectif'] = effectif
          except:
              print("effectif non trouvee pour l'URL:", url)
          try:
              commerciaux = chiffres_cles.find_element(By.CSS_SELECTOR, "li.ep-key-value.ep-epages-business-details-sales-staff dl.ep-key-value__content dd.ep-key-value__value").text
              url_specific_data['commerciaux'] = commerciaux
          except:
            print("commerciaux non trouvee pour l'URL:", url)
          try:
            ca_export = chiffres_cles.find_element(By.CSS_SELECTOR, "li.ep-key-value.ep-epages-business-details-export-sales dl.ep-key-value__content dd.ep-key-value__value").text
            url_specific_data['ca_export'] = ca_export
          except:
            print("ca_export non trouvee pour l'URL:", url)

        except Exception as e:
           print("information not found for URL:", url)
        #add to list
        all_data.append(url_specific_data)
    except Exception as e:
        continue

  return all_data


# Main function
if __name__ == "__main__":
    company_urls = collect_url(url)
    data= collect_info(company_urls)
    df = pd.DataFrame(data)
    df.to_excel('companies_info.xlsx', index=False)
    print("Scraping completed and data saved to companies_info.xlsx")

# Quit WebDriver
driver.quit()
