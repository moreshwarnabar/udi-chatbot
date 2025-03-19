import { Button } from '@/components/ui/button';
import logo from '@/assets/ASU.png';

interface NavbarProps {
  isLoggedIn: boolean;
  loginHandler: () => void;
}

const Navbar = ({ isLoggedIn, loginHandler }: NavbarProps) => {
  return (
    <nav className="flex justify-between items-center p-3 text-asu_maroon shadow-md">
      <img src={logo} alt="asu logo" className="h-10 w-auto" />
      <div className="text-xl font-bold uppercase">UDI Chatbot</div>

      <Button
        onClick={loginHandler}
        className="bg-asu_blue/90 text-white px-4 py-2 rounded-lg hover:bg-asu_blue hover:cursor-pointer"
      >
        {isLoggedIn ? 'Logout' : 'Login'}
      </Button>
    </nav>
  );
};

export default Navbar;
