import { Builder, By, until } from "selenium-webdriver";
import * as firefox from "selenium-webdriver/firefox.js";
import "geckodriver";
import fs from "fs";

async function sleep(timeout) {
  return new Promise((res) => {
    setTimeout(() => {
      res();
    }, timeout);
  });
}
export async function getAccountToken(user, pass) {
  const fireopts = new firefox.Options()
    //.headless()
    .windowSize({ width: 1280, height: 720 })
    .setAcceptInsecureCerts(true);
  //setting headless later pls don't fuck up
  const firebuild = await new Builder()
    .setFirefoxOptions(fireopts)
    .forBrowser("firefox")
    .build();
  try {
    await firebuild.get("https://old.reddit.com/login");
    //TODO: replace with process.argv ----------------------->>>>
    await firebuild.findElement(By.id("user_login")).sendKeys(`${user}`);
    const pswd = await firebuild.findElement(By.id("passwd_login"));
    await pswd.sendKeys(`${pass}`);
    await pswd.submit();
    await sleep(4000);
    await firebuild.get("https://new.reddit.com/r/place");
    const val = await firebuild
      .executeScript(
        `
    async function test () {
        const response = await fetch("https://new.reddit.com/r/place");
        const responseText = await response.text();
        console.log(responseText.match(/"accessToken":"(\\"|[^"]*)"/)[1])
        return responseText.match(/"accessToken":"(\\"|[^"]*)"/)[1];
}; return test();`
      )
    return val;
  } catch (e) {
    console.error(e);
  } finally {
    firebuild.close();
  }
}

console.log(await getAccountToken(process.argv[2], process.argv[3]));
