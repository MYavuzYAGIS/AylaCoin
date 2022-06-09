//SPDX-License-Identifier: GPL-3.0-or-later
// Aylacoin'n ICO

//version
pragma solidity ^0.8.14;

contract aylacoin_ico {
    // Introduce the max num of aylacoin for sale
    uint32 public max_aylacoins = 1000000;

    // conversion USD/AC parity
    uint32 public usd_to_aylacoin = 100;

    //amount of Aylacoins bought by investors
    uint32 public total_aylacoins_bought = 0;
}
