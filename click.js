let clicks = 0;

let listeningForClicks = false;

const click = () => {
  clicks = clicks + 1;

  if (listeningForClicks === false) {
    let timeout = setTimeout(() => {
      if (clicks === 1) {
        clicks = 0;
        listeningForClicks = false;

        roll();
      }

      if (clicks >= 2) {
        clicks = 0;
        listeningForClicks = false;

        nextRound();
      }
    }, 2000);
  }

  listeningForClicks = true;
};

document.querySelector("button").addEventListener("click", click);
