import { useRef } from "react"
import { login , register} from "../API/DefaultAPI"
import toast from 'react-hot-toast';


const Login = ({ setLogin }) => {

    const phonenumber = useRef()

    const RegisterHandler = () => {

        let phoneNumberRegex = new RegExp('^(\\+98|0)?9\\d{9}$')
        let result = phoneNumberRegex.test(phonenumber.current.value)

        let newPhoneNumber;
        if (phonenumber.current.value.slice(0,2) === '09'){
            newPhoneNumber = '+989' + phonenumber.current.value.slice(2, 11)
            
        }
        
        
        if (!result){    
                toast.error('شماره وارد شده معتبر نیست.',{
                    id: 'clipboard',
                })
                
            
        }else{

            const loading = toast.loading('')
            register(newPhoneNumber).then(() => {
                setLogin(true)
                toast.dismiss(loading)
                toast.success('با موفقیت وارد شدید')
            }).catch(err => {
                toast.dismiss(loading)
                toast.error('شماره ثبت نشده است.')
            })

            
            // Service("POST",  newPhoneNumber.toString() ).then( (res) => {
            //     toast.dismiss(loading)
            //     if (res.status === 201) {
                    
            //         setLogin(true)
            //         // toast.dismiss(loading)
            //         toast.success('با موفقیت وارد شدید',  {id : loading})
            //         console.log(res.data)
            //         localStorage.setItem('access',res.data.access)
            //         localStorage.setItem('refresh', res.data.refresh)
            //         localStorage.setItem("access_expiration", res.data["access_expiration"])
            //         localStorage.setItem("refresh_expiration", res.data["refresh_expiration"])
            //     }
        
            // }).catch((err) => {
            //     // toast.remove(loading)
            //     toast.error('خطایی رخ داد دوباره سعی کنید', {id : loading})
            //     console.log(err);
            //     if (err.status === 401){
            //     }
                
    
            // })
            // toast.success('با موفقیت وارد شدید')
            
            
        }

        

    }



    return (

        <div id="loginForm" className=" flex flex-col no-wrap justify-center items-center basis-1/2 w-full p-2 gap-2 bg-white rounded-2xl">
            <div className="flex flex-col w-full">
                {/* <label className="self-start mb-2 font-[600] text-gray-700 texg-lg" dir="rtl" htmlFor="login_user_name"></label> */}
                <input placeholder="شماره موبایل" ref={phonenumber} id="login_user_name" type="tel" className="bg-gray-100 h-[50px] rounded-2xl w-full outline-none p-3 text-center mb-1" />
            </div>

            <button type="button" onClick={() => RegisterHandler()} className=" w-full h-[50px] rounded-2xl bg-sky-800 text-white text-lg">ادامه</button>
        </div>



    )
}

export default Login