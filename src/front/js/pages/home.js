import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import "../../styles/index.css";
import { useNavigate } from "react-router-dom";

export const Home = () => {
  const navigate = useNavigate();
  const { store, actions } = useContext(Context);

  useEffect(() => {
    store.token && navigate("/private");
  });

  return (
    <>
      <div className="text-center body">
        <div className="h-100 row justify-content-center">
          <div className="col-12 text-center">
            <table style={{ height: "100%" }}>
              <tbody>
                <tr>
                  <td className="align-middle">
                    <h1
                      className="text-white animate-charcter"
                      style={{ fontSize: "100px", margin: "220px" }}
                    >
                      Welcome to the Zusset World
                    </h1>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
};
