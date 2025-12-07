/**
 * SCRIPT PRINCIPAL - Sistema de Gestión de Casos y Expedientes
 * Maneja la lógica del frontend y comunicación con el backend
 */

// ============================================================================
// CONFIGURACIÓN API
// ============================================================================

const API_BASE_URL = "http://localhost:8000/api";

// ============================================================================
// VARIABLES GLOBALES
// ============================================================================

let clienteSeleccionado = null;
let casoSeleccionado = null;
let expedienteSeleccionado = null;
let modoEdicion = false;

// ============================================================================
// INICIALIZACIÓN
// ============================================================================

document.addEventListener("DOMContentLoaded", () => {
    inicializarEventosPestañas();
    inicializarEventosCaso();
    inicializarEventosExpediente();
    inicializarEventosModal();
});

// ============================================================================
// EVENTO: CAMBIO DE PESTAÑA
// ============================================================================

function inicializarEventosPestañas() {
    const tabBtns = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabBtns.forEach((btn) => {
        btn.addEventListener("click", () => {
            // Remover clase active de todos
            tabBtns.forEach((b) => b.classList.remove("active"));
            tabContents.forEach((t) => t.classList.remove("active"));

            // Agregar clase active al seleccionado
            btn.classList.add("active");
            const tabId = btn.getAttribute("data-tab");
            document.getElementById(tabId).classList.add("active");

            // Si es expediente, cargar datos
            if (tabId === "expediente" && casoSeleccionado) {
                cargarExpedientesCaso(casoSeleccionado.noCaso);
            }
        });
    });
}

// ============================================================================
// EVENTOS - PESTAÑA CASO
// ============================================================================

function inicializarEventosCaso() {
    const btnBuscarCliente = document.getElementById("btnBuscarCliente");
    const btnCrearCaso = document.getElementById("btnCrearCaso");
    const btnGuardarCaso = document.getElementById("btnGuardarCaso");
    const nombreApellidoInput = document.getElementById("nombreApellidoCliente");
    const casosActivosSelect = document.getElementById("casosActivos");

    // Buscar cliente por nombre y apellido
    btnBuscarCliente.addEventListener("click", async () => {
        const nombreApellido = nombreApellidoInput.value.trim().split(" ");
        if (nombreApellido.length < 2) {
            alert("Por favor ingrese nombre y apellido");
            return;
        }

        const nombre = nombreApellido[0];
        const apellido = nombreApellido.slice(1).join(" ");

        try {
            const response = await fetch(
                `${API_BASE_URL}/cliente/buscar/${nombre}/${apellido}`
            );
            const clientes = await response.json();

            if (clientes.length === 0) {
                alert("Cliente no encontrado");
                document.getElementById("resultadosBusquedaCliente").classList.remove("mostrar");
                return;
            }

            // Mostrar resultados de búsqueda
            mostrarResultadosBusqueda(clientes);
        } catch (error) {
            console.error("Error en búsqueda:", error);
            alert("Error al buscar cliente");
        }
    });

    // Crear nuevo caso
    btnCrearCaso.addEventListener("click", async () => {
        if (!clienteSeleccionado) {
            alert("Por favor seleccione un cliente");
            return;
        }

        // Habilitar campos para nuevo caso
        document.getElementById("fechaInicio").disabled = false;
        document.getElementById("especializacion").disabled = false;
        document.getElementById("valor").disabled = false;
        btnGuardarCaso.disabled = false;

        // Cargar especializaciones en el dropdown
        cargarEspecializaciones();

        modoEdicion = true;
        casoSeleccionado = null;
    });

    // Guardar caso
    btnGuardarCaso.addEventListener("click", async () => {
        if (!clienteSeleccionado) {
            alert("Cliente no seleccionado");
            return;
        }

        const fechaInicio = document.getElementById("fechaInicio").value;
        const valor = document.getElementById("valor").value;
        const codEspecializacion = document.getElementById("especializacion").value;

        if (!fechaInicio || !valor || !codEspecializacion) {
            alert("Complete todos los campos requeridos");
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/caso/crear`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    fechaInicio: fechaInicio,
                    fechaFin: null,
                    valor: valor,
                    codEspecializacion: codEspecializacion,
                    codCliente: clienteSeleccionado.codCliente,
                }),
            });

            const result = await response.json();
            if (result.success) {
                alert(`Caso ${result.noCaso} creado exitosamente`);
                casoSeleccionado = result;
                document.getElementById("noCaso").value = result.noCaso;
                limpiarFormularioCaso();
                btnCrearCaso.disabled = false;
            }
        } catch (error) {
            console.error("Error al crear caso:", error);
            alert("Error al crear caso");
        }
    });

    // Cambiar caso en dropdown
    casosActivosSelect.addEventListener("change", async (e) => {
        const noCaso = e.target.value;
        if (noCaso) {
            await cargarCaso(parseInt(noCaso));
        }
    });

    // Permitir búsqueda con Enter
    nombreApellidoInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            btnBuscarCliente.click();
        }
    });
}

// ============================================================================
// EVENTOS - PESTAÑA EXPEDIENTE
// ============================================================================

function inicializarEventosExpediente() {
    const btnCrearExpediente = document.getElementById("btnCrearExpediente");
    const btnGuardarExpediente = document.getElementById("btnGuardarExpediente");
    const btnImprimirCaso = document.getElementById("btnImprimirCaso");
    const btnAdjuntarDoc = document.getElementById("btnAdjuntarDoc");

    btnCrearExpediente.addEventListener("click", async () => {
        if (!casoSeleccionado) {
            alert("Seleccione un caso primero");
            return;
        }

        // Habilitar campos para nuevo expediente
        document.getElementById("fechaEtapa").disabled = false;
        document.getElementById("abogado").disabled = false;
        document.getElementById("ciudad").disabled = false;
        document.getElementById("entidad").disabled = false;
        document.getElementById("impugnacion").disabled = false;
        document.getElementById("suceso").disabled = false;
        document.getElementById("resultado").disabled = false;
        document.getElementById("btnAnteriorSuceso").disabled = false;
        document.getElementById("btnSiguienteSuceso").disabled = false;
        document.getElementById("btnAnteriorResultado").disabled = false;
        document.getElementById("btnSiguienteResultado").disabled = false;
        document.getElementById("btnAdjuntarDoc").disabled = false;
        btnGuardarExpediente.disabled = false;

        modoEdicion = true;
    });

    btnGuardarExpediente.addEventListener("click", async () => {
        // Aquí irá la lógica para guardar el expediente
        alert("Funcionalidad de guardar expediente");
    });

    btnImprimirCaso.addEventListener("click", () => {
        // Aquí irá la lógica para imprimir maestro-detalle
        alert("Funcionalidad de imprimir caso con expediente");
    });

    btnAdjuntarDoc.addEventListener("click", () => {
        // Aquí irá la lógica para adjuntar documentos PDF
        alert("Funcionalidad de adjuntar documentos");
    });
}

// ============================================================================
// EVENTOS - MODAL
// ============================================================================

function inicializarEventosModal() {
    const modal = document.getElementById("modalEditor");
    const closeBtn = document.querySelector(".close");
    const btnGuardarModal = document.getElementById("btnGuardarModal");

    closeBtn.addEventListener("click", () => {
        modal.style.display = "none";
    });

    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });

    btnGuardarModal.addEventListener("click", () => {
        const campo = document.getElementById("modalTextarea").getAttribute("data-campo");
        const valor = document.getElementById("modalTextarea").value;
        document.getElementById(campo).value = valor;
        modal.style.display = "none";
    });

    // Double-click para editar en textos largos
    document.getElementById("suceso").addEventListener("dblclick", () => {
        abrirEditorModal("suceso", "Editar Suceso");
    });

    document.getElementById("resultado").addEventListener("dblclick", () => {
        abrirEditorModal("resultado", "Editar Resultado");
    });
}

// ============================================================================
// FUNCIONES AUXILIARES - CLIENTE
// ============================================================================

function mostrarResultadosBusqueda(clientes) {
    const container = document.getElementById("resultadosBusquedaCliente");
    container.innerHTML = "";

    clientes.forEach((cliente) => {
        const div = document.createElement("div");
        div.className = "resultado-item";
        div.textContent = `${cliente.nomCliente} ${cliente.apellCliente} - ${cliente.nDocumento}`;
        div.addEventListener("click", () => seleccionarCliente(cliente));
        container.appendChild(div);
    });

    container.classList.add("mostrar");
}

function seleccionarCliente(cliente) {
    clienteSeleccionado = cliente;
    document.getElementById("nDocumento").value = cliente.nDocumento;
    document.getElementById("nombreApellidoCliente").value =
        `${cliente.nomCliente} ${cliente.apellCliente}`;
    document.getElementById("resultadosBusquedaCliente").classList.remove("mostrar");
    document.getElementById("btnCrearCaso").disabled = false;

    // Cargar últimos casos activos
    cargarCasosActivos(cliente.codCliente);
}

async function cargarCasosActivos(codCliente) {
    try {
        const response = await fetch(`${API_BASE_URL}/caso/activos/${codCliente}`);
        const casos = await response.json();

        const select = document.getElementById("casosActivos");
        select.innerHTML = '<option value="">-- Seleccionar --</option>';

        casos.forEach((caso) => {
            const option = document.createElement("option");
            option.value = caso.noCaso;
            option.textContent = `Caso ${caso.noCaso} - ${caso.valor}`;
            select.appendChild(option);
        });

        if (casos.length > 0) {
            // Cargar automáticamente el primer caso
            select.value = casos[0].noCaso;
            cargarCaso(casos[0].noCaso);
        }
    } catch (error) {
        console.error("Error al cargar casos activos:", error);
    }
}

// ============================================================================
// FUNCIONES AUXILIARES - CASO
// ============================================================================

async function cargarCaso(noCaso) {
    try {
        const response = await fetch(`${API_BASE_URL}/caso/${noCaso}`);
        const caso = await response.json();

        casoSeleccionado = caso;
        document.getElementById("noCaso").value = caso.noCaso;
        document.getElementById("fechaInicio").value = caso.fechaInicio;
        document.getElementById("fechaFin").value = caso.fechaFin || "";
        document.getElementById("valor").value = caso.valor;
        document.getElementById("especializacion").value = caso.codEspecializacion;
        document.getElementById("noCasoExp").value = caso.noCaso;

        // Si el caso tiene fecha fin, deshabilitar edición
        if (caso.fechaFin) {
            document.getElementById("fechaInicio").disabled = true;
            document.getElementById("especializacion").disabled = true;
            document.getElementById("valor").disabled = true;
            document.getElementById("btnGuardarCaso").disabled = true;
        }
    } catch (error) {
        console.error("Error al cargar caso:", error);
        alert("Error al cargar caso");
    }
}

async function cargarEspecializaciones() {
    try {
        const response = await fetch(`${API_BASE_URL}/especializacion/`);
        const especializaciones = await response.json();

        const input = document.getElementById("especializacion");
        input.value = "";
    } catch (error) {
        console.error("Error al cargar especializaciones:", error);
    }
}

function limpiarFormularioCaso() {
    document.getElementById("noCaso").value = "";
    document.getElementById("fechaInicio").value = "";
    document.getElementById("fechaFin").value = "";
    document.getElementById("especializacion").value = "";
    document.getElementById("valor").value = "";
    document.getElementById("nDocumento").value = "";
    modoEdicion = false;
}

// ============================================================================
// FUNCIONES AUXILIARES - EXPEDIENTE
// ============================================================================

async function cargarExpedientesCaso(noCaso) {
    try {
        const response = await fetch(`${API_BASE_URL}/expediente/caso/${noCaso}`);
        const expedientes = await response.json();

        if (expedientes.length > 0) {
            // Cargar el primer expediente
            cargarExpedienteDetalle(expedientes[0].consecExpe);
            document.getElementById("btnCrearExpediente").disabled = true;
        } else {
            document.getElementById("btnCrearExpediente").disabled = false;
            limpiarFormularioExpediente();
        }
    } catch (error) {
        console.error("Error al cargar expedientes:", error);
    }
}

async function cargarExpedienteDetalle(consecExpe) {
    try {
        const response = await fetch(`${API_BASE_URL}/expediente/${consecExpe}`);
        const expediente = await response.json();

        expedienteSeleccionado = expediente;
        document.getElementById("consecExpe").value = expediente.consecExpe;
        document.getElementById("noEtapa").value = expediente.codEtapa;
        document.getElementById("fechaEtapa").value = expediente.fechaEtapa;
        document.getElementById("nomEtapa").value = expediente.nomEtapa;
        document.getElementById("suceso").value = expediente.conSuceso || "";
        document.getElementById("resultado").value = expediente.conResul || "";

        // Deshabilitar campos de lectura
        document.getElementById("consecExpe").disabled = true;
        document.getElementById("noEtapa").disabled = true;
        document.getElementById("fechaEtapa").disabled = true;
        document.getElementById("nomEtapa").disabled = true;
    } catch (error) {
        console.error("Error al cargar expediente detalle:", error);
    }
}

function limpiarFormularioExpediente() {
    document.getElementById("consecExpe").value = "";
    document.getElementById("noEtapa").value = "";
    document.getElementById("fechaEtapa").value = "";
    document.getElementById("nomEtapa").value = "";
    document.getElementById("instancia").value = "";
    document.getElementById("abogado").value = "";
    document.getElementById("ciudad").value = "";
    document.getElementById("entidad").value = "";
    document.getElementById("impugnacion").value = "";
    document.getElementById("suceso").value = "";
    document.getElementById("resultado").value = "";
}

// ============================================================================
// FUNCIONES AUXILIARES - MODAL
// ============================================================================

function abrirEditorModal(campo, titulo) {
    const modal = document.getElementById("modalEditor");
    const textarea = document.getElementById("modalTextarea");

    document.getElementById("modalTitle").textContent = titulo;
    textarea.setAttribute("data-campo", campo);
    textarea.value = document.getElementById(campo).value;
    modal.style.display = "flex";
}

// ============================================================================
// MANEJO DE ERRORES Y LOGS
// ============================================================================

// Interceptor de errores global
window.addEventListener("error", (event) => {
    console.error("Error global:", event.error);
});

// Log de inicialización
console.log("✓ Script cargado correctamente");
console.log(`✓ API Base URL: ${API_BASE_URL}`);
