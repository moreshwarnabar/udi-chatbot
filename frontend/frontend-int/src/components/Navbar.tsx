import { Button } from '@/components/ui/button';
import logo from '@/assets/ASU.png';

interface NavbarProps {
  isLoggedIn: boolean;
  loginHandler: () => void;
}

const Navbar = ({ isLoggedIn, loginHandler }: NavbarProps) => {
  return (
    <nav className="flex justify-between items-center p-3 bg-gray-900 text-white shadow-md">
      <img src={logo} alt="asu logo" className="h-10 w-auto" />
      <div className="text-xl font-bold text-blue-400">UDI Chatbot</div>

      <Button
        onClick={loginHandler}
        className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 hover:cursor-pointer"
      >
        {isLoggedIn ? 'Logout' : 'Login'}
      </Button>
    </nav>
  );
};

export default Navbar;
