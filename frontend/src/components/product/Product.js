import Login from "../login/Login"
import CartInfo from "../CartInfo/CartInfo"
import {useEffect, useState} from "react"
import {useParams} from "react-router-dom"
import toast from "react-hot-toast"
import {verifyUser} from "../API/DefaultAPI"


const base_url = 'https://scarfly.ir/api';
const getData = async (productID) => {
    return await fetch(`${base_url}/products/retrieve/${productID}/`)
}

export default function Product() {
    const [loginState, setLoginState] = useState(false)
    const [product, setProduct] = useState()
    let params = useParams()
    useEffect(() => {
        verifyUser().then(async (r) => setLoginState(r));

        getData(params.productID).then(async (res) => {
            if (res.status === 200) {
                setProduct(await res.json());
                return
            } else if (res.status === 404) toast.error('محصول یافت نشد')
            console.log(res)
            console.log(res.data)
            toast.error('خطایی رخ داد .\n دوباره سعی کنید.')
        })
    }, [params])

    return (
        <div className="block  flex-col bg-gray-200">
            <div className="flex flex-col w-full h-full p-6 justify-between items-center gap-4">
                <div id="productDetail" className="  rounded-2xl bg-white p-2 gap-4 flex flex-col ">
                    <img src={product?.image} className="w-full h-fit rounded-2xl" alt={product?.name}/>
                    <div className="flex flex-col justify-between gap-4">
                        <p className="font-[600] text-gray-800 texg-lg">{product?.name}</p>
                        <span className="whitespace-nowrap font-[700] text-gray-800 texg-lg self-end">{product?.sell_price} تومان</span>
                    </div>
                </div>

                {loginState ? <CartInfo productID={params.productID}/> : <Login setLogin={setLoginState}/>}

            </div>
        </div>
    )
}