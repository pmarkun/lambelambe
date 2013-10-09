/*
  rasterizeElement.js
  
  This file is a helper script for use with phantomJS (http://phantomjs.org/) similar to rasterize.js
  allowing you to rasterize elements of a web page by specifying a selector.

  Author - Stephen James 
  Twitter - @stephenhjames
  GitHub - https://github.com/stephen-james
  
*/

console.log("");
console.log("== rasterizeElement.js =====================================================");

var page = require('webpage').create(),
    
    defaults = {
        // default values for rasterisation if not passed in as parameters
        viewPortSize : { 
            width : 1280,
            height : 768
        },
        zoomFactor : 1,
        paperSize : {
            format : "A4",
            orientation : "portrait",
            margin : "1cm"
        } 
    },
    
    options = parseScriptArguments();

function extendObject(targetObjectToExtend, sourceObject) {
    // extends the target object by copying properties that don't already exist (by key) from the source object
    for(var propertyToCheck in sourceObject) {
        if (!targetObjectToExtend.hasOwnProperty(propertyToCheck)) {
            targetObjectToExtend[propertyToCheck] = sourceObject[propertyToCheck];
        }
    }
}
    
function raiseErrorAndExit(message, showOptions) {
    // helper method to write errors to the console and terminate the process
    console.log(message);
    if (showOptions != false) {
        console.log("[info] - you called rasterizeElement with these options : " + JSON.stringify(options));
    }
    phantom.exit();
};
    
function parseScriptArguments() {
    // parses the script arguments and builds up the options for the rasterization operation
    var system = require('system'),
        clonedArguments = system.args.slice(),
        options;

    // clean up args to not include the initial argument to phantomjs (which is this script name)       
    clonedArguments.shift();
    
    // validate...
    if (clonedArguments.length < 3 || clonedArguments.length > 6) {
        console.log("    Usage: rasterizeElement.js fromUrl renderElementBySelector toDestinationFilename [viewPortSize] [zoomFactor] [paperSize]");
        console.log("");        
        console.log("    eg. (basic usage)");   
        console.log("");        
        console.log("    phantomjs rasteriseElement.js http://www.awebsite.com \"#idOfElementToSelect\" output.png");               
        console.log("");                
        raiseErrorAndExit("", false);
    }
    else {
        
        options = {
            addressOfPageToRender : clonedArguments[0],
            elementSelector : clonedArguments[1],
            outputFileName : clonedArguments[2]         
        };
        
        // handle optional arguments
        if (clonedArguments.length > 3) { 
            console.log("[info] - interpretting viewPortSize");     
            try {
                options["viewPortSize"] = JSON.parse(clonedArguments[3])
            }
            catch (err) {
                raiseErrorAndExit("[error] - Invalid value passed for viewPortSize (" + clonedArguments[3] + ")");
            }
        }
        if (clonedArguments.length > 4) { options["zoomFactor"] = clonedArguments[4]; }
        if (clonedArguments.length > 5) { 
            console.log("[info] - interpretting paperSize");                
            try {
                options["paperSize"] = JSON.parse(clonedArguments[5])
            }
            catch (err) {
                raiseErrorAndExit("[error] - Invalid value passed for paperSize (" + clonedArguments[5] + ")");
            }
        }       
        
        extendObject(options, defaults);

        // if we are rendering to pdf, we must consider this a paper render
        options.paperRender = options.outputFileName.substr(-4) === ".pdf";
        
        return options;
    }
}

page.open(options.addressOfPageToRender, function (loadStatus) {
    
    if (loadStatus !== 'success') {
        raiseErrorAndExit("[error] - Unable to load the address! (" + options.addressOfPageToRender + ")");
    } 

    page.zoomFactor = options.zoomFactor;
    page.viewportSize = options.viewPortSize;
    
    // evaluate the clipping rectangle of the element we would like to select and rasterise
    var elementClipRect = page.evaluate(function(selector) {
        var elementToRasterize = document.querySelector(selector);
        
        if (!elementToRasterize) {
            return;
        }
        else {
            var elementRect = elementToRasterize.getBoundingClientRect();
        
            return {
                top:    elementRect.top,
                left:   elementRect.left,
                width:  elementRect.width,
                height: elementRect.height
            };
        }
    }, options.elementSelector);
    
    if (!elementClipRect) {
        raiseErrorAndExit("[error] - Unable to locate element for provided selector! (" + options.elementSelector + ")");
    }
    else
    {
        page.clipRect = elementClipRect;
        console.log("[info] - applying clipping rectangle for selection " + JSON.stringify(elementClipRect));
    }

    
    if (options.paperRender) {
        page.paperSize = options.paperSize;
    }
    
    page.render(options.outputFileName);
    
    console.log("[info] - done");       

    phantom.exit();

});