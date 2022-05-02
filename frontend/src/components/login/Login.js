import {useRef} from "react"
import {loginRegister} from "../API/DefaultAPI"
import toast from 'react-hot-toast';


const Login = ({setLogin}) => {
    const phoneNumber = useRef()

    const RegisterHandler = async () => {
        const phoneNumberRegex = new RegExp('^(\\+98|0)?9\\d{9}$')
        let phoneNumberValue = phoneNumber.current.value;

        if (!phoneNumberRegex.test(phoneNumberValue)) {
            toast.error('شماره وارد شده معتبر نیست.', {id: 'clipboard',})
        }

        if (phoneNumberValue.slice(0, 1) === '0') {
            phoneNumberValue = '+98' + phoneNumberValue.slice(1, 11)
        }

        const loading = toast.loading('چند لحظه...')
        const loginResponse = await loginRegister(phoneNumberValue)
        setLogin(loginResponse);
        toast.dismiss(loading)
        if (loginResponse) {
            toast.success('با موفقیت وارد شدید')
        }
    }

    return (
        <div id="loginForm" className=" flex flex-col no-wrap justify-center items-center basis-1/2 w-full p-2 gap-2 bg-white rounded-2xl">
            <div className="flex flex-col w-full">
                {/* <label className="self-start mb-2 font-[600] text-gray-700 texg-lg" dir="rtl" htmlFor="login_user_name"></label> */}
                <input placeholder="شماره موبایل" ref={phoneNumber} id="login_user_name" type="tel" className="bg-gray-100 h-[50px] rounded-2xl w-full outline-none p-3 text-center mb-1"/>
            </div>

            <button type="button" onClick={() => RegisterHandler()} className=" w-full h-[50px] rounded-2xl bg-sky-800 text-white text-lg">ادامه</button>
        </div>
    )
}

export default Login