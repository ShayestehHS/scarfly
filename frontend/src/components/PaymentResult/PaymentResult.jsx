import {useSearchParams} from "react-router-dom";
import axios from "axios";
import {verifyUser} from "../API/DefaultAPI";
import {useEffect, useState} from "react";

const base_url = 'https://scarfly.ir/api';

export default function PaymentResult() {
    console.log("PaymentResult component")
    const [searchParams, setSearchParams] = useSearchParams();
    const [isStatusOk, setIsStatusOk] = useState(searchParams.get('Status') === 'OK');
    const [orderData, setOrderData] = useState({})
    const authority = searchParams.get("Authority");
    useEffect(() => {
        if (isStatusOk) {
            verifyUser()
                .then(isUserValid => {
                    if (!isUserValid) throw new Error('User have to authenticate')

                    return axios.patch(base_url + `/orders/update/status/${authority}/`,
                        {},
                        {headers: {'Authorization': 'Bearer ' + localStorage.getItem('access')}});
                })
                .then(res => setOrderData(res.data))
                .catch(err => {
                    if (err.response) {
                        if (err.response.status === 400) {
                            setIsStatusOk(false);
                            return;
                        } else {
                            console.log(err.response);
                            console.log(err.response.data);
                        }
                    }
                    console.log(err);
                })
        }
    }, [isStatusOk])

    console.log('end render PaymentResult')
    return (
        <>
            <div className=" h-screen w-full flex items-center justify-center gap-4 flex-col">
                {isStatusOk ? (
                    <>
                        <svg className="h-20 bg-green-700 fill-white rounded-full p-[10px]"
                             xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"
                        >
                            <path d="M480.969 128.969L208.969 400.969C204.281 405.656 198.156 408 192 408S179.719 405.656 175.031 400.969L31.031 256.969C21.656 247.594 21.656 232.406 31.031 223.031S55.594 213.656 64.969 223.031L192 350.062L447.031 95.031C456.406 85.656 471.594 85.656 480.969 95.031S490.344 119.594 480.969 128.969Z"/>
                        </svg>
                        <div className="p-4 text-xl font-bold  w-3/4  flex gap-4 justify-center itens-center">
                            <p className="text-green-800 text-center">
                                خرید با موفقیت انجام شد
                            </p>

                        </div>
                    </>
                ) : (
                    <>
                        <svg className="h-20 bg-red-500 fill-white rounded-full p-[10px]"
                             xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 512"
                        >
                            <path d="M308.281 347.717C323.906 363.342 323.906 388.655 308.281 404.28C292.647 419.914 267.339 419.9 251.719 404.28L160 312.561L68.281 404.28C52.647 419.914 27.339 419.9 11.719 404.28C-3.906 388.655 -3.906 363.342 11.719 347.717L103.438 255.999L11.719 164.281C-3.906 148.656 -3.906 123.344 11.719 107.719S52.656 92.094 68.281 107.719L160 199.437L251.719 107.719C267.344 92.094 292.656 92.094 308.281 107.719S323.906 148.656 308.281 164.281L216.562 255.999L308.281 347.717Z"
                                  className="fa-secondary"/>
                        </svg>

                        <div className="p-4 text-xl font-bold  w-3/4  flex gap-4 justify-center itens-center">
                            <p className="text-red-800 text-center">خرید با مشکل مواجه شد</p>
                        </div>
                    </>
                )}
                {orderData.address ? (
                    <div>
                        <p>کد پیگیری: {orderData.payment_id}</p>
                        <p>محصولات: </p>
                        <div>
                            {orderData.products.map((item, i) => (
                                <p key={i}>نام محصول: {item.name}</p>
                            ))}
                        </div>
                        <p>جمع فاکتور: {orderData.sum_price}</p>
                        <p>مبلغ پرداختی: {orderData.pay_amount}</p>
                        <p>کد تخفیف: {orderData.offer_key ? orderData.offer_key : "ندارد"}</p>
                        <p>آدرس: {orderData.address}</p>
                        <p>تاریخ ثبت سفارش: {orderData.timestamp}</p>
                    </div>
                ) : (<></>)}
            </div>
        </>
    );
}
