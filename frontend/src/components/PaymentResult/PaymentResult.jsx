import { useSearchParams } from "react-router-dom";

export default function Home() {
  const [searchParams, setSearchParams] = useSearchParams();
  console.log(searchParams.get("Authority"));

  return (
    <>
      <div className=" h-screen w-full flex items-center justify-center gap-4 flex-col">
        {searchParams.get("Status") === "OK" ? (
          <>
          <svg
                className="h-20 bg-green-700 fill-white rounded-full p-[10px]"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 512 512"
              >
                <path d="M480.969 128.969L208.969 400.969C204.281 405.656 198.156 408 192 408S179.719 405.656 175.031 400.969L31.031 256.969C21.656 247.594 21.656 232.406 31.031 223.031S55.594 213.656 64.969 223.031L192 350.062L447.031 95.031C456.406 85.656 471.594 85.656 480.969 95.031S490.344 119.594 480.969 128.969Z" />
              </svg>
            <div className="p-4 text-xl font-bold  w-3/4  flex gap-4 justify-center itens-center">
              <p className="text-green-800 text-center">
                خرید با موفقیت انجام شد
              </p>
              
            </div>
          </>
        ) : (
          <>
            <svg
              className="bg-red-500 fill-white h-20 rounded-full py-[13px] px-[23px]"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 320 512"
            >
              <defs></defs>
              <path
                d="M308.281 347.717C323.906 363.342 323.906 388.655 308.281 404.28C292.647 419.914 267.339 419.9 251.719 404.28L160 312.561L68.281 404.28C52.647 419.914 27.339 419.9 11.719 404.28C-3.906 388.655 -3.906 363.342 11.719 347.717L103.438 255.999L11.719 164.281C-3.906 148.656 -3.906 123.344 11.719 107.719S52.656 92.094 68.281 107.719L160 199.437L251.719 107.719C267.344 92.094 292.656 92.094 308.281 107.719S323.906 148.656 308.281 164.281L216.562 255.999L308.281 347.717Z"
                className="fa-secondary"
              />
            </svg>

            <div className="p-4 text-xl font-bold  w-3/4  flex gap-4 justify-center itens-center">
              <p className="text-red-800 text-center">خرید با مشکل مواجه شد</p>
            </div>
          </>
        )}
        <div className="bg-sky-300 text-lg w-1/2 rounded-2xl text-center justify-center gap-2 p-2 flex flex-row   items-center">
          <svg
            className="h-8 fill-sky-600  self-start"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 496 512"
          >
            <path d="M248 8C111 8 0 119 0 256s111 248 248 248 248-111 248-248S385 8 248 8zm121.8 169.9l-40.7 191.8c-3 13.6-11.1 16.9-22.4 10.5l-62-45.7-29.9 28.8c-3.3 3.3-6.1 6.1-12.5 6.1l4.4-63.1 114.9-103.8c5-4.4-1.1-6.9-7.7-2.5l-142 89.4-61.2-19.1c-13.3-4.2-13.6-13.3 2.8-19.7l239.1-92.2c11.1-4 20.8 2.7 17.2 19.5z" />
          </svg>
          <p className="text-sky-900 font-bold text-xl self-center">اتصال به ربات</p>
        </div>
      </div>
    </>
  );
}
