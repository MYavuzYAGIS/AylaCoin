//SPDX-License-Identifier: GPL-3.0-or-later
// Aylacoin'n ICO

//version
pragma solidity ^0.8.7;

contract aylacoin_ico {
    // Introduce the max num of aylacoin for sale
    uint32 public max_aylacoins = 1000000;

    // conversion USD/AC parity
    uint32 public usd_to_aylacoin = 100;

    //amount of Aylacoins bought by investors
    uint32 public total_aylacoins_bought = 0;

    // mapping from investor address to its equity in Aylacoin and USD
    mapping(address => uint32) equity_aylacoins;
    mapping(address => uint32) equity_usd;

    // check if investor can buy aylacoin
    modifier can_buy_aylacoin(uint32 usd_invested) {
        require(
            usd_invested * usd_to_aylacoin + total_aylacoins_bought <=
                max_aylacoins
        );
        _;
    }

    // getting the equity in aylacoins of an investor
    function equity_in_aylacoins(address investor)
        external
        view
        returns (uint32)
    {
        return equity_aylacoins[investor];
    }

    // getting the equity in usd of an investor

    function equity_in_usd(address investor) external view returns (uint32) {
        return equity_usd[investor];
    }

    // Buying Aylacoin
    function buy_aylacoin(address investor, uint32 usd_invested)
        external
        can_buy_aylacoin(usd_invested)
    {
        uint32 aylacoin_bought = usd_invested * usd_to_aylacoin;
        equity_aylacoins[investor] += aylacoin_bought;
        equity_usd[investor] = equity_aylacoins[investor] / 100;
    }
}
