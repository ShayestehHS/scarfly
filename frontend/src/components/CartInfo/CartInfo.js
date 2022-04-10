import { useRef, useEffect } from "react"
import { createOrder } from "../API/DefaultAPI";




const CartInfo = ({ loginState, productID }) => {

    const nameRef = useRef(),
        familyRef = useRef(),
        addressRef = useRef(),
        postallCodeRef = useRef();

    const cartRef = useRef()
    useEffect(() => {
        cartRef.current && cartRef.current.scrollIntoView()
    }, [loginState])


    const payFunc = () => {

        
        
        const order = {
            "product": productID,
            "address": addressRef.current.value,
            "postal_code": postallCodeRef.current.value,
        }
        
        createOrder(order).then(res => {
            window.location.href = `https://www.zarinpal.com/pg/StartPay/${res.data.authority}`
        })
        
    }


    return (
        <div ref={cartRef} id="CartInfo" className="w-full flex flex-col gap-10 bg-white rounded-2xl p-4 basis-1/2 mb-12" >
            <div className="flex flex-col gap-4 ">
                <label className="">نام</label>
                <input ref={nameRef} type="text" placeholder="نام" className="bg-gray-100 focus:border border-gray-100 focus:bg-white h-[50px] rounded-2xl w-full overflow-hidden outline-none p-4 text-right" />
                <label className="">نام خانوادگی</label>
                <input ref={familyRef} type="text" placeholder="نام خانوادگی" className="bg-gray-100 focus:border border-gray-100 focus:bg-white h-[50px] rounded-2xl w-full overflow-hidden outline-none p-4 text-right" />
            </div>
            <div className="flex flex-col gap-4">
                <label className="">آدرس</label>
                <textarea ref={addressRef} type="text" placeholder="آدرس" className="bg-gray-100 focus:border border-gray-100 focus:bg-white h-[100px] rounded-2xl w-full overflow-hidden outline-none p-4 text-right" />
                <label className="">کد پستی</label>
                <input ref={postallCodeRef} type="text" placeholder="10 رقم" className="bg-gray-100 focus:border border-gray-100 focus:bg-white h-[50px] rounded-2xl w-full overflow-hidden outline-none p-4 text-right" />
            </div>
            {/* <div className="flex flex-col gap-2 ">
                <label>روش ارسال</label>
                <select className="bg-gray-100 overflow-none focus:bg-white h-[50px] w-full  rounded-2xl p-2 focus:border border-gray-100 ">
                    <option >
                        پست
                    </option>

                </select>

            </div> */}
            <button onClick={payFunc} type="button" className="h-[50px] rounded-2xl bg-lime-700 text-white text-lg fixed bottom-2 w-[86%] self-center">پرداخت</button>

        </div>


    )
}

export default CartInfo