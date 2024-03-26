"""
Incepeti sa luati din testele pe care le-ati facut la cele trei sesiuni de selectori (Selectori_P1, Selectori_P2, 
Selectori_P3) si implementati-le in metode de test folosind framework-ul unit test. 

Rulati testele si observati rezultatele
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MyTestCase(unittest.TestCase):
    driver = None
    LINK_URL = 'https://www.elefant.ro/'

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    def setUp(self):
        self.driver.get(self.LINK_URL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(3)
        self.wait_and_click(By.CSS_SELECTOR, 'button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
        self.driver.implicitly_wait(5)

    def tearDown(self):
        self.driver.delete_all_cookies()
        self.driver.implicitly_wait(1)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # def wait_and_click(self, by, locator):
    #     element = self.driver.find_element(by, locator)
    #     element.click()

    def wait_and_click(self, by, locator):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((by, locator)))
            element.click()
        except Exception as e:
            print(f"Eroare la apasarea elementului: {e}")

    def wait_and_send_keys(self, by, locator, keys):
        element = self.driver.find_element(by, locator)
        element.send_keys(keys)

    def wait_send_keys_submit(self, by, locator, keys):
        element = self.driver.find_element(by, locator)
        element.send_keys(keys)
        element.submit()

    def wait_element_is_visible(self, by, locator):
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.visibility_of_element_located((by, locator)))

    def get_login_page(self):
        self.driver.get('https://www.elefant.ro/login')
        self.driver.implicitly_wait(3)

    # def test_accept_cookies(self):
    #     self.wait_and_click(By.CSS_SELECTOR, 'button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
    #     self.driver.implicitly_wait(2)

    def test_search_product(self):
        self.wait_send_keys_submit(By.NAME, 'SearchTerm', 'iphone 14')

    def test_check_results(self):
        self.wait_send_keys_submit(By.NAME, 'SearchTerm', 'iphone 14')
        self.driver.implicitly_wait(5)

        results = self.driver.find_elements(By.CSS_SELECTOR, '.product-title')
        # assert len(results) >= 10, 'Mai putin de 10 rezultate gasite'
        self.assertGreaterEqual(len(results), 10, 'Mai putin de 10 rezultate gasite')

    def test_get_cheapest_product(self):
        self.wait_send_keys_submit(By.NAME, 'SearchTerm', 'iphone 14')
        self.driver.implicitly_wait(3)

        lista_elemente_nume = self.driver.find_elements(By.CSS_SELECTOR, '.product-title')
        lista_elemente_pret = self.driver.find_elements(By.CLASS_NAME, 'current-price ')

        lista_nume_pret = [
            (nume.text, float(pret.text.replace(' lei', '').replace(',', '.')))
            for nume, pret in zip(lista_elemente_nume, lista_elemente_pret)
            if pret.text != 'N/A'
        ]

        lista_nume_pret.sort(key=lambda x: x[1])
        pret_minim = lista_nume_pret[0][1]
        nume_produs_pret_minim = lista_nume_pret[0][0]

        print("Pretul cel mai mic este:", pret_minim)
        print("Numele produsului cu pretul cel mai mic este:", nume_produs_pret_minim)

    def test_get_page_title(self):
        page_title = self.driver.title
        # assert 'elefant' in page_title.lower()
        self.assertIn('elefant', page_title.lower(), 'Eroare titlu pagina')

    def test_input_invalid_user_password(self):
        self.wait_and_click(By.XPATH, "//a[@data-toggle='collapse']//i[contains(text(), 'face')]")
        self.wait_element_is_visible(By.XPATH, "//a[@class='my-account-login btn btn-primary btn-block']")
        self.wait_and_click(By.XPATH, "//a[@class='my-account-login btn btn-primary btn-block']")
        self.wait_element_is_visible(By.ID, 'ShopLoginForm_Login')
        self.wait_and_send_keys(By.ID, 'ShopLoginForm_Login', 'gresit@test.com')
        self.wait_and_send_keys(By.ID, 'ShopLoginForm_Password', 'gresita')

    def test_failed_login_message(self):
        self.get_login_page()
        self.wait_and_send_keys(By.ID, 'ShopLoginForm_Login', 'gresit@test.com')
        self.wait_and_send_keys(By.ID, 'ShopLoginForm_Password', 'gresita')
        self.wait_and_click(By.NAME, 'login')
        self.wait_element_is_visible(By.NAME, 'login')

        login_button = self.driver.find_element(By.NAME, 'login')
        # assert login_button.is_displayed() is True
        self.assertTrue(login_button.is_displayed())

        eroare_asteptata = 'Adresa dumneavoastră de email / Parola este incorectă. Vă rugăm să încercați din nou.'
        eroare_primita = self.driver.find_element(By.XPATH, "//div[@role='alert']").text
        # assert eroare_primita == eroare_asteptata, "Mesaj eroare diferit de cel asteptat"
        self.assertEqual(eroare_asteptata, eroare_primita, "Mesaj eroare diferit de cel asteptat")

    def test_login_button_disabled(self):
        self.get_login_page()

        email = self.driver.find_element(By.ID, 'ShopLoginForm_Login')
        email.send_keys('invalid')
        self.driver.implicitly_wait(3)

        login_button = self.driver.find_element(By.NAME, 'login')
        # assert login_button.is_enabled() is False
        self.assertFalse(login_button.is_enabled())

if __name__ == '__main__':
    unittest.main()
