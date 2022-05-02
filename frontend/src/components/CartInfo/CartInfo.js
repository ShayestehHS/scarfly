import {useRef, useEffect, useState} from "react"
import {createOrder, retrieveUserData} from "../API/DefaultAPI";
import toast from "react-hot-toast";

const CartInfo = ({loginState, productID}) => {
    const [name, setName] = useState();
    const [family, setFamily] = useState();

    retrieveUserData(setName, setFamily) // ToDo: Big optimization

    const nameRef = useRef(),
        familyRef = useRef(),
        addressRef = useRef(),
        offerKeyRef = useRef(),
        postalCodeRef = useRef();

    const cartRef = useRef()
    useEffect(() => {
        cartRef.current && cartRef.current.scrollIntoView()
    }, [loginState])

    const payFunc = () => {
        const order = {
            "products": [productID],
            "address": addressRef.current.value,
            "postal_code": postalCodeRef.current.value,
            "offer_key": offerKeyRef.current.value,
        }
        console.log(order)
        createOrder(order).then(res => {
            console.log("Create order")
            console.log(res)
            if (res.status !== 201) {
                if (res.status === 404 && res.data.offer_key != null) {
                    toast.error('کد تخفیف وارد شده صحیح نمی باشد.');
                    offerKeyRef.current.value = '';
                    return;
                }
                toast.error("مشکلی پیش آمده. لطثا دوباره امتحان کنید");
                console.log(res);
                window.location.reload()
                return;
            }
            window.location.href = `https://www.zarinpal.com/pg/StartPay/${res.data.authority}`
        })
    }

    return (
        <div ref={cartRef} id="CartInfo" className="w-full flex flex-col gap-10 bg-white rounded-2xl p-4 basis-1/2 mb-12">
            <div className="flex flex-col gap-4 ">
                <label className="">نام</label>
                <input type="text" placeholder="نام"
                       ref={nameRef} defaultValue={name}
                       disabled={'disabled' ? name != null : ''}
                       className="bg-gray-100 focus:border border-gray-100 focus:bg-white h-[50px] rounded-2xl w-full overflow-hidden outline-none p-4 text-right"/>
                <label className="">نام خانوادگی</label>
                <input type="text" placeholder="نام خانوادگی"
                       ref={familyRef} defaultValue={family}
                       disabled={'disabled' ? family != null : ''}
                       className="bg-gray-100 focus:border border-gray-100 focus:bg-white h-[50px] rounded-2xl w-full overflow-hidden outline-none p-4 text-right"/>
            </div>
            <div className="flex flex-col gap-4">
                <label className="">آدرس</label>
                <textarea ref={addressRef} placeholder="آدرس"
                          className="bg-gray-100 focus:border border-gray-100 focus:bg-white h-[100px] rounded-2xl w-full overflow-hidden outline-none p-4 text-right"/>
                <label className="">کد پستی</label>
                <input type="text" placeholder="ده رقم ( اختیاری )"
                       ref={postalCodeRef}
                       className="bg-gray-100 focus:border border-gray-100 focus:bg-white h-[50px] rounded-2xl w-full overflow-hidden outline-none p-4 text-right"/>
                <label className="">کد تحفیف</label>
                <input type="text" ref={offerKeyRef}
                       className="bg-gray-100 focus:border border-gray-100 focus:bg-white h-[50px] rounded-2xl w-full overflow-hidden outline-none p-4 text-right"/>
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