import { useEffect, useState } from "react";

const SharedLinks = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const isLogin = localStorage.getItem('login');
    setIsLoggedIn(!!isLogin);
  }, []);

  // Return empty component - no shared links functionality
  return null;
};

export default SharedLinks;