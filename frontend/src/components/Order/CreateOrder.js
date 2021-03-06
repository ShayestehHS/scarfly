import Login from "../login/Login"
import CartInfo from "../CartInfo/CartInfo"
import {useEffect, useState} from "react"
import React from "react"
import {verifyUser} from "../API/DefaultAPI"
import Carousel from "./Carousel";

function CreateOrder() {
    console.log("CreateOrder component")

    const [loginState, setLoginState] = useState(false);
    useEffect(() => {
            verifyUser().then(r => setLoginState(r));
        }, []
    )
    const queryString = require('query-string');
    const listProductID = queryString.parse(window.location.search).productID;


    return (
        <div className="block  flex-col bg-gray-200">
            <div className="flex flex-col w-full h-full p-6 justify-between items-center gap-4">
                <Carousel listProductID={listProductID}/>

                {loginState ? <CartInfo productID={listProductID}/> : <Login setLogin={setLoginState}/>}

            </div>
        </div>
    )
}

export default React.memo(CreateOrder)