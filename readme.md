# File handling 

input file(json, txt, csv) ---> parser(dictionary format) ---> output file(json)

#  Workflow

# Step-by-Step Flow
1. **Config.json** defines input type, output type  
2. **InputHandlerFactory** picks the correct handler:
   - Local file (JSON, CSV, TXT)
   - Cloud (future)
   - Database (future)  
3. **ParserFactory** selects the parser:
   - `JSONParser`
   - `CSVParser`
   - `TXTParser`
   - `DBParser` (future)  
4. **OutputHandlerFactory** decides where results are saved:
   - Local filesystem
   - Cloud storage (future)
   - Database (future)  
5. **main.py** orchestrates the whole pipeline.

---

### 📊 Workflow Diagram


                ┌────────────────────┐
                │    config.json     │
                └─────────┬──────────┘
                          │
                          ▼
               ┌──────────────────────┐
               │ InputHandlerFactory  │
               └─────────┬────────────┘
                         │
         ┌───────────────┼────────────────┐
         ▼                                ▼
 LocalFileInputHandler          DatabaseInputHandler
 (JSON, CSV, TXT)               (future)  
         ▼                               ▼
      raw data ----------------------- raw data
                         │
                         ▼
               ┌──────────────────────┐
               │   ParserFactory      │
               └─────────┬────────────┘
                         │
         ┌───────────────┼────────────────┐
         ▼                                ▼
    JSONParser                       CSVParser
    TXTParser                        DBParser (future)
                         ▼
               structured Python dict
                         │
                         ▼
               ┌──────────────────────┐
               │ OutputHandlerFactory │
               └─────────┬────────────┘
                         │
         ┌───────────────┼────────────────-----------------┐
         ▼                                                 ▼
 LocalOutputHandler                                 CloudOutputHandler
                    DatabaseOutputHandler (future)       (future) 
