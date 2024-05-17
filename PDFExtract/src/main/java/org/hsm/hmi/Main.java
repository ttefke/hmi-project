package org.hsm.hmi;

import com.sun.net.httpserver.HttpServer;
import org.apache.pdfbox.Loader;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

import java.io.*;
import java.net.InetSocketAddress;
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

            // Modules in json
            TextOutput o = new TextOutput(moduleStringModels);
            String httpResponse = o.asJSON();

            // Start HTTP Server: http://localhost:8080/modules_json
            HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
            server.createContext("/modules_json", httpExchange -> {
                OutputStream output = httpExchange.getResponseBody();
                httpExchange.getResponseHeaders().set("Content-Type", "application/json");
                httpExchange.sendResponseHeaders(200, httpResponse.getBytes().length);
                output.write(httpResponse.getBytes());
                output.flush();
                output.close();
            });

            // Modules in SQL:
            String sqlResponse = "CREATE TABLE \"acs_modules\" (\n" +
                    "\t\"file_loc\"\tTEXT,\n" +
                    "\t\"title\"\tTEXT, \n" +
                    "\t\"instructor\"\tTEXT, \n" +
                    "\t\"learning_obj\"\tTEXT, \n" +
                    "\t\"course_contents\"\tTEXT, \n" +
                    "\t\"teaching-methods\"\tTEXT, \n" +
                    "\t\"prerequisites\"\tTEXT, \n" +
                    "\t\"readings\"\tTEXT, \n" +
                    "\t\"applicability\"\tTEXT, \n" +
                    "\t\"workload\"\tTEXT, \n" +
                    "\t\"credits\"\tTEXT, \n" +
                    "\t\"evaluation\"\tTEXT, \n" +
                    "\t\"time\" \tTEXT, \n" +
                    "\t\"frequency\"\tTEXT, \n" +
                    "\t\"duration\"\tTEXT, \n" +
                    "\t\"course_type\"\tTEXT, \n" +
                    "\t\"remarks\" \tTEXT\n" +
                    ");";
            for (ModuleStringModel model: moduleStringModels) {
                sqlResponse += "\n";
                sqlResponse += new SQLInsertStatementGenerator().createStatement(model);
                sqlResponse += "\n";
            }

            final String finalSQLResponse = sqlResponse;
            server.createContext("/modules_sql", httpExchange -> {
                OutputStream output = httpExchange.getResponseBody();
                httpExchange.getResponseHeaders().set("Content-Type", "text/plain");
                httpExchange.sendResponseHeaders(200, finalSQLResponse.getBytes().length);
                output.write(finalSQLResponse.getBytes());
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