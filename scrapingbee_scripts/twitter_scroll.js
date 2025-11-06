// twitter_scroll.js
await page.waitForTimeout(8000);          // wait for 8 s for the JS to settle
await page.evaluate(_ => window.scrollBy(0, 2000));  // scroll a bit
await page.waitForTimeout(2000);          // give extra time for new tweets
