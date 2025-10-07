EDIT: There may be other additional wallets that were not included in the snapshot this program uses. This is only a partial list of wallets that were originally on the doc as some wallets had complicated tx's that would goof up the calculations.

Instructions: 

Run script: python app.py

Stop: Cntrl+C OR Get-Process -Name python -ErrorAction SilentlyContinue | Stop-Process -Force

View the web UI at: http://localhost:8000/leaderboard.html

I tried my best but it started to get really complicated since not everyone used new wallets and some of us made additional transfers between when the snapshot was taken and when we got sent the 32k gala.
 
Some of the addresses did not make a single trade so they're all at 0% change.

How is it calculated? Took a snapshot on 9/22 , these balances are compared with the current balances.
GUSDC/GUSDT = $1
GALA priced from coingecko

32,894 GALA is subtracted from every address before total calculation.(Thats what we were all sent)

eth|2f7c7e2D248d8784fC186A5Cd2d5aD0e4E6dAE1f received 60k gala on snapshot day before the 32k gala, so an additional 60k gala has been subtracted from this entry

eth|FBc1e9e5A82F555c445F17c95fB4B96Bd05c2047 was not added as it was sent gala twice, though it did return it I did not include it in the snapshot at the time. I can still add this one back in, just have to take a new snapshot of it and update the code to include that address.

eth|B951E44209E52Eae85C9E2f4Af62B8bc8bad9fC2 was not added, as it was the address that sent us the gala, the numbers would be messed up

client|64f8caf887fd8551315d8509 is messed up as well as its not a new wallet and I think it's factoring in the allowance somewhere(cant see in screenshot but its negative 10k USD)

