# BlockBets

# How to setup and run the aplication
Demo application is available at https://self-assured-webbed-lemming.anvil.app/. Before you can interact with the application you need to connect to MetaMask and Sepolia following step (1) below. If you want to manually compile the application from scratch follow steps (1) through (3) below. 

## 1) Connecting to MetaMask and Sepolia
1) Install the MetaMask Chrome extension
2) Add a a new network in MetaMask
    - RPC: `https://eth-sepolia.g.alchemy.com/v2/9H0qMRUY9eb3brffXCJAoNXXK94v7E4F` 
    - Chain ID: `11155111`
    - Currency Symbol: `ETH`
    - Block Explorer: `https://sepolia.etherscan.io/`
3) Acquire free test network ETH from `https://sepoliafaucet.com/`


## 2) Running the Blockchain Smart Contract using Remix IDE
1) Upload the smart contract, `BlockBets/blockchain_code/BetApp.sol`, to Remix IDE. 
2) Compile the contract
3) Deploy the contract using MetaMask Injected provider
4) Update the contract address and ABI at the top of `BlockBets/client_code/SmartContract.py`


## 3) Running the frontend 
### Option 1 - Running locally
1) Clone the Github repository.
2) Install the Anvil app server using `pip install anvil-app-server`
3) Start the server using `anvil-app-server --app <app-directory-name>` replacing `<app-directory-name>` with the name of the cloned directory. 
    - Note you may need to install the Java virtual machine to successfully start the server. On Linux you can use `sudo apt-get install openjdk-8-jdk libpq-dev` to instal JVM. 
4) Navigate to `localhost`

### Option 2 - Running via Anvil
1) Go to the [Anvil Editor](https://anvil.works/build?utm_source=github:app_README) (you might need to sign up for a free account) and click on “Clone from GitHub” (underneath the “Blank App” option):
<img src="https://anvil.works/docs/version-control-new-ide/img/git/clone-from-github.png" alt="Clone from GitHub"/>

2) Enter the URL of this GitHub repository. If you're not yet logged in, choose "GitHub credentials" as the authentication method and click "Connect to GitHub".
<img src="https://anvil.works/docs/version-control-new-ide/img/git/clone-app-from-git.png" alt="Clone App from Git modal"/>

3) Finally, click "Clone App". This app will then be in your Anvil account, ready for you to run. Find the **Run** button at the top-right of the Anvil editor. The application will start. 
<img src="https://anvil.works/docs/img/run-button-new-ide.png"/>


