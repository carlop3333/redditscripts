import { Builder, By, until } from "selenium-webdriver";
import * as firefox from "selenium-webdriver/firefox.js";
import "geckodriver";
import fetch from "node-fetch";
import fs from "fs";
import * as captcha from "2captcha";

function random(min, max) {
  // min and max included
  return Math.floor(Math.random() * (max - min + 1) + min);
}

//this one is for saving mails
const MailMap = new Map();

async function loop(i) {
  return new Promise(async (res) => {
    var creds = random(10000,0x7fffffff) + ":" + "foobar"
    console.log(creds)
  const fireopts = await new firefox.Options()
    .windowSize({
      width: 1280,
      height: 720,
    })
    .setPreference("network.proxy.type", 1)
    .setPreference("network.proxy.socks", `${creds}@127.0.0.1`)
    .setPreference("network.proxy.socks_port", 9050)
    .setPreference("network.proxy.ssl", `127.0.0.1`)
    .setPreference("network.proxy.ssl_port", 9049)
    .setPreference("browser.privatebrowsing.autostart", true);
  const firebuild = await new Builder()
    .forBrowser("firefox")
    .setFirefoxOptions(fireopts)
    .build();
  try {
    const config = JSON.parse(
      fs.readFileSync("config.json", { encoding: "utf-8" })
    );
    //shit from random psswrd
    const keys = await fetch(
      "https://www.psswrd.net/api/v1/password/?length=17&lower=1&upper=0&int=1&special=0"
    );
    const pwsd = await keys.json();
    //mailshit
    const mail = `${config.your_email}+${i}@gmail.com`;
    await firebuild.get("https://old.reddit.com/register");
    //user shit
    const x = await firebuild.findElement(By.id("user_reg"));
    x.sendKeys(`${config.prefix}_${pwsd.password}`);
    
    await firebuild.findElement(By.id("passwd_reg")).sendKeys(pwsd.password);
    await firebuild.findElement(By.id("passwd2_reg")).sendKeys(pwsd.password);
    await firebuild.findElement(By.id("email_reg")).sendKeys(mail);
    //makes the captcha appear
    await firebuild.actions().click(x).perform();
    /**
     * @type {string}
     */
    const USERNAME = config.prefix + "_" + pwsd.password
    
    console.log(pwsd.password);
    fs.writeFileSync(
      "out.txt",
      "\nUsername: " + `${USERNAME.slice(0, 20)} ` + "Password'n Email: " + `${pwsd.password}_${mail} \n`,
      { flag: "a+" }
    ); 
    setTimeout(async () => {
      //im sacrifycing myself good luck
      console.log("awaiting captcha");
      const captch = new captcha.Solver("1234567890qwertyuiop", 15);
      const result = await captch.recaptcha(
        "6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-XC",
        "https://old.reddit.com/register"
      );
      await firebuild.executeScript(
        `document.getElementById("g-recaptcha-response").innerHTML=arguments[0];`,
        result.data
      );
      await firebuild
        .findElement(By.className("c-btn c-btn-primary c-pull-right"))
        .click();
      console.log("DONEE!");
      setTimeout(() => {
        res();
      }, 5000);
    }, 6800);
    MailMap.set(`${mail}`, `${USERNAME}_${pwsd.password}`);   
  } finally {
    //firebuild.close()
  }
  })
}

(async function start() {
    for (var i = 17; i <= 18; i++) {
      await loop(i);
    }  
})();

MailMap.forEach((val) => {
  console.log(val);
});
