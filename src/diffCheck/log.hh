#pragma once

#include <loguru.hpp>

namespace diffCheck
{
    class Log
    {
    public:
        Log() { Init(); }
        ~Log() { Shutdown(); }

    private:
        // void Init();
        // void Shutdown();
        void Init()
        {
            // int argc = 1;
            // char* argv[] = { "loguru", nullptr };
            // loguru::init(argc, argv);
            // loguru::add_file("diffCheckEvery.log", loguru::Truncate, loguru::Verbosity_MAX);
            // loguru::add_file("diffCheckErrors.log", loguru::Truncate, loguru::Verbosity_ERROR);

            // loguru::g_stderr_verbosity = 1;
            // loguru::g_colorlogtostderr = true;
            // loguru::g_preamble = false;
        }

        void Shutdown()
        {
            // loguru::shutdown();
        }
    };
}

#ifndef SILENT_LOGGING
    #define DIFFCHECK_INFO(message) LOG_F(INFO, message)
    #define DIFFCHECK_WARN(message) LOG_F(WARNING, message)
    #define DIFFCHECK_ERROR(message) LOG_F(ERROR, message)
    #define DIFFCHECK_FATAL(message) LOG_F(FATAL, message)
#else
    #define DIFFCHECK_INFO
    #define DIFFCHECK_WARN
    #define DIFFCHECK_ERROR
    #define DIFFCHECK_FATAL
#endif