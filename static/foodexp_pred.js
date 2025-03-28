function predict_foodexp() {
    var salary = document.getElementById("salary").value;
    console.log(salary); 
    document.getElementById("expenditure").innerText =
        "Predicted Food Expenditure: " + (0.4851 * salary + 147.4);
}
