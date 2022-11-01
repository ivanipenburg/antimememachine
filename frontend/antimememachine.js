console.log("Welcome to Anti-Meme Machine")

function addBorder () {
    let images = document.getElementsByClassName('ImageBox-image')
    for (let img of images) {
        img.style.border = "5px solid red";
    }
}


function predictImages () {
    addBorder()

    const input = document.getElementsByClassName('ImageBox-image')

    for (let i = 0; i < input.length; i++) {
        let src = input[i].src
        console.log(src)

        fetch(src).then(
            res => res.blob()
        ).then(
            blob => {
                console.log("Extension log")
                console.log(blob)
                var file = new File([blob], src, {
                    type: blob.type,
                })
                console.log(file)
                
                const formData = new FormData()

                formData.append('file', file)

                fetch('http://localhost:5000/predict', {
                    method: 'POST',
                    mode: 'cors',
                    body: formData, // Don't use JSON.stringify!!
                })
                .then(response => response.json())
                .then(json => console.log(json))
                .catch(err => console.log(err))
                
            }
        )
    }
}

predictImages()

// const observer = new MutationObserver((mutations) => {
//     mutations.forEach((mutation) => {
//         if (mutation.addedNodes && mutation.addedNodes.length > 0) {
//             predictImages()
//         }
//     });
// });

// observer.observe(document.body, {
//     childList: true,
//     subtree: true
// });
