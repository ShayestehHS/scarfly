import Login from "../login/Login"
import CartInfo from "../CartInfo/CartInfo"
import { useState, useEffect } from "react"
import { useParams } from "react-router-dom"
import toast from "react-hot-toast"
import {  verify } from "../API/DefaultAPI"


const getData = async (productID) => {
    const response = await fetch(`https://api.scarfly.ir/products/${productID}/`)
    return response
}

export default function Product() {
    const [loginState, setLoginState] = useState(false)
    const [product, setproduct] = useState()
    let params = useParams()



        useEffect( () => {

            verify().then(res => {
                if(res.status === 200){
                    setLoginState(true)
                }
                
            })

            getData(params.productID).then(async (e) => {

                if(e.status === 200){
                    const data = await e.json()
                    setproduct(data)
                   
                    return
                }
                if(e.status === 404){
                    toast.error('محصول یافت نشد')
                    return
                }
                if(e.status === 400){
                    toast.error('شماره قبلا وارد شده')
                    return
                }
                toast.error(
                    'خطایی رخ داد .\n دوباره سعی کنید.'
                )
                
                
                
            })
            //////////

            

            
            
         

        }, [params])
        
       
        

    

    return(
        <div className="block  flex-col bg-gray-200">
            <div className="flex flex-col w-full h-full p-6 justify-between items-center gap-4">
                <div id="productDetail" className="  rounded-2xl bg-white p-2 gap-4 flex flex-col ">
                <img src={product?.image} className="w-full h-fit rounded-2xl" alt={product?.name} />
                <div className="flex flex-col justify-between gap-4">
                    <p className="font-[600] text-gray-800 texg-lg">{product?.name}</p>
                    <span className="whitespace-nowrap font-[700] text-gray-800 texg-lg self-end">{product?.sell_price} تومان</span>
                </div>
                </div> 
                
                {loginState ? <CartInfo productID={params.productID} /> : <Login setLogin={setLoginState}/>}
                
            </div>
        </div>
    )
}

