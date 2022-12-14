"use strict";
document.addEventListener("DOMContentLoaded", () => {
    const iframe = document.createElement("iframe");
    let selectedLand = "",
        landings = [],
        pageNum = 0;

    document.getElementById("downloadTxt").addEventListener("click", (e) => {
        e.preventDefault();
        if (!selectedLand) {
            showError("Лендинг не выбран");
        } else {
            window.location.href = `static/generated/${selectedLand[2]}/text.txt`;
        }
    });

    document.getElementById("downloadZip").addEventListener("click", (e) => {
        e.preventDefault();
        if (!selectedLand) {
            showError("Лендинг не выбран");
        } else {
            let data = {
                folder: selectedLand[2],
                land: selectedLand[3],
            };
            fetchData("landgen/zip", data, (err, ans) => {
                if (err) {
                    console.error("Произошла ошибка", err);
                } else {
                    if (ans.status === "ok") {
                        console.log(ans);
                        window.location.href = `static/generated/${selectedLand[2]}/${selectedLand[3]}.zip`;
                    } else {
                        showError(ans.message);
                    }
                }
            });
        }
    });

    document.getElementById("landgenForm").addEventListener("submit", (e) => {
        e.preventDefault();
        document.getElementById("submitLandgen").disabled = true;
        document.getElementById("preview").innerText = "Pending...";
        let data = {
            product_name: e.target.product_name.value,
            product_description: e.target.product_description.value,
            feature_1: e.target.feature_1.value,
            feature_2: e.target.feature_2.value,
            feature_3: e.target.feature_3.value,
            language: e.target.language.value,
        };
        fetchData("landgen", data, (err, ans) => {
            if (err) {
                console.error("Произошла ошибка", err);
                document.getElementById("submitLandgen").disabled = false;
            } else {
                if (ans.status === "ok") {
                    document.getElementById("submitLandgen").disabled = false;
                    if (Array.isArray(ans.message)) landings.push(...ans.message);
                    else throw new Error("Неизвестный ответ от сервера");
                    selectedLand = checkLandPath(landings[pageNum]);

                    iframe.sandbox = "";
                    iframe.width = "100%";
                    iframe.height = "100%";
                    iframe.src = landings[pageNum];
                    document.getElementById("preview").innerText = "";
                    document.getElementById("preview").appendChild(iframe);
                    document.getElementById("pageCount").innerText = landings.length;
                } else {
                    document.getElementById("submitLandgen").disabled = false;
                    showError(ans.message);
                }
            }
        });
    });

    document.getElementById("leftArrow").addEventListener("click", () => {
        if (pageNum > 0) {
            pageNum--;
            iframe.src = landings[pageNum];
            document.getElementById("pageNum").innerText = pageNum + 1;
            selectedLand = checkLandPath(landings[pageNum]);
        }
    });

    document.getElementById("rightArrow").addEventListener("click", () => {
        if (pageNum < landings.length - 1) {
            pageNum++;
            iframe.src = landings[pageNum];
            document.getElementById("pageNum").innerText = pageNum + 1;
            selectedLand = checkLandPath(landings[pageNum]);
        }
    });
});

function checkLandPath(path) {
    if (path?.includes("/")) return path.split("/");
    else if (path?.includes("\\")) return path.split("\\");
    else showError("Невадидный адрес");
    return false;
}
function showError(text = "Ошибка") {
    const errorToastEl = new bootstrap.Toast(document.getElementById("errorToastEl"));
    document.getElementById("errorToastEl").querySelector(".toast-body").innerText = text;
    errorToastEl.show();
}

function showSuccess(text = "Успех") {
    const successToastEl = new bootstrap.Toast(document.getElementById("successToastEl"));
    document.getElementById("successToastEl").querySelector(".toast-body").innerText = text;
    successToastEl.show();
}

function fetchData(path, data, callback) {
    fetch(path, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
        },
        cache: "no-cache",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        body: JSON.stringify(data),
    })
        .catch((err) => showError(err))
        .then(async (resolve) => {
            try {
                if (resolve.status === 200) {
                    let ans = await resolve.json();
                    callback(null, ans);
                } else {
                    throw new Error("Ответ сети был не ok.");
                }
            } catch (error) {
                showError("Ошибка HTTP: ", resolve.status, error.message);
                console.log(error.message);
                callback(error);
            }
        });
}
