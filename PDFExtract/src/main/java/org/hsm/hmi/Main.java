package org.hsm.hmi;

import com.sun.net.httpserver.HttpServer;
import org.apache.pdfbox.Loader;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

import java.io.*;
import java.net.InetSocketAddress;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.List;
import java.util.concurrent.Executors;

public class Main {
    public static void main(String[] args) {
        new Main().run();
    }

    public void run() {
        try {
            // Read in modules
            InputStream inputStream;
            inputStream = getClass().getResourceAsStream("module_manual_IMACS.pdf");
            File pdfFile = File.createTempFile("pdfextract", ".pdf");
            OutputStream outputStream = new FileOutputStream(pdfFile);
            if (inputStream != null) {
                inputStream.transferTo(outputStream);
                inputStream.close();
            }

            PDDocument document = Loader.loadPDF(pdfFile);
            String text = new PDFTextStripper().getText(document);
            TextMining textToString = new TextMining(text);
            List<ModuleStringModel> moduleStringModels = textToString.convert();
            TextOutput o = new TextOutput(moduleStringModels);
            String httpResponse = o.asJSON();

            // Start HTTP Server: http://localhost:8080/modules
            HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
            server.createContext("/modules", httpExchange -> {
                OutputStream output = httpExchange.getResponseBody();
                httpExchange.getResponseHeaders().set("Content-Type", "application/json");
                httpExchange.sendResponseHeaders(200, httpResponse.getBytes().length);
                output.write(httpResponse.getBytes());
                output.flush();
                output.close();
            });
            server.setExecutor(Executors.newFixedThreadPool(4));
            server.start();
            System.out.println("Started HTTP server");
        } catch (IOException | NullPointerException e) {
            throw new RuntimeException(e);
        }
    }
}